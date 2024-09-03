from PIL import Image
from celery import shared_task
from io import BytesIO
import uuid
import os
import requests
from model import db, File_status
from storage import addFile
import shutil


@shared_task()
def process_images(request_id, file_path, processed_folder):
    try:
        import pandas as pd
        df = pd.read_csv(file_path)
        results = []

        for _, row in df.iterrows():
            s_no = row['S. No.']
            product_name = row['Product Name']
            input_image_urls = row['Input Image Urls'].split(',')
            output_image_urls = []

            for url in input_image_urls:
                url = url.strip()
                response = requests.get(url)
                image = Image.open(BytesIO(response.content))
                processed_filename = str(uuid.uuid4().hex) + ".jpg"
                processed_file_path = os.path.join(processed_folder, processed_filename)

                image.save(processed_file_path, format='JPEG', quality=50)
                
                #upload to S3 bucket
                image_url = addFile(request_id+"/"+processed_filename, processed_file_path)

                output_image_urls.append(image_url)
                
            results.append({
                    'S. no.':s_no,
                    'Product Name': product_name,
                    'Input Image Urls': ','.join(input_image_urls),
                    'Output Image Urls': ','.join(output_image_urls)
                })
            
        results_df = pd.DataFrame(results)
        csv_filename = request_id + "_output.csv"
        csv_file_path = os.path.join(processed_folder, csv_filename)
        results_df.to_csv(csv_file_path, index=False)

        #upload to S3 bucket
        csv_url = addFile(request_id+"/"+csv_filename, csv_file_path)

        file_status = File_status.query.get(request_id)
        if file_status:
            file_status.status = 'Completed'
            file_status.final_file_path = csv_url
            db.session.commit()
        #remove the local directory after uploading it to the S3 bucket
        shutil.rmtree(processed_folder)

    except Exception as e:
        print(e)
        file_status = File_status.query.get(request_id)
        if file_status:
            file_status.status = 'Failed'
            db.session.commit()
        #remove the local directory if the process failed    
        shutil.rmtree(processed_folder)