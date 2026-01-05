from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name', 'phone_number')
    def validate_name_and_phone(self, key, value): #validates that name is not empty and that 2 authors cannot have the same name
        if key == 'name':
            existing_author = Author.query.filter_by(name=value).first() # Check for existing author with the same name
            if existing_author:
                raise ValueError("Author with this name already exists")
            if not value or value.strip() == "":
                raise ValueError("Name cannot be empty")
        elif key == 'phone_number':
            if value:
                if not value.isdigit() or len(value) != 10:
                    raise ValueError("Phone number must be exactly 10 digits")
        return value
        

        
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title', 'content', 'category', 'summary')
    def validate_post_fields(self,key, value):
        if key =='content':
            if not value or len(value)<250 :
                raise ValueError("Content must be at least 250 characters long")
        if key == 'category':
            allowed_categories = ['Fiction', 'Non-Fiction']
            if value not in allowed_categories:
                raise ValueError("Category must be one of the following: 'Fiction', 'Non-Fiction'")
        if key == 'summary':
            if len(value) > 250 and len(value)>0:
                raise ValueError("Summary must be at most 250 characters long")
        if key =='title':
            allowed_post_titles = ["Won't Believe", "Secret", "Top", "Guess"]
            if not any(phrase in value for phrase in allowed_post_titles):
                raise ValueError("Title must contain one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'")


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
