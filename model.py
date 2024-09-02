from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class File_status(db.Model):
    __tablename__ = 'Image_Process'
    id = db.Column(db.String(36), primary_key=True)
    original_file_path = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    final_file_path = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<FileRequest {self.id}>'