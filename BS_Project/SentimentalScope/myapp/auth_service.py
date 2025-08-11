from .mongodb_connection import mongodb
import hashlib
import secrets
from datetime import datetime
import re
from bson.objectid import ObjectId

class AuthService:
    def __init__(self):
        self.users_collection = mongodb.get_collection('User')
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password):
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        return True, "Password is valid"
    
    def hash_password(self, password, salt=None):
        """Hash password using SHA-256 with salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Combine password and salt
        combined = f"{password}{salt}"
        
        # Hash using SHA-256
        hashed = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        
        return f"{salt}:{hashed}"
    
    def verify_password(self, password, hashed_password):
        """Verify password against hash"""
        try:
            salt, hash_value = hashed_password.split(':')
            return self.hash_password(password, salt) == hashed_password
        except ValueError:
            return False
    
    def user_exists(self, email):
        """Check if user exists by email"""
        try:
            user = self.users_collection.find_one({"email": email})
            return user is not None
        except Exception as e:
            print(f"Error checking if user exists: {e}")
            return False
    
    def create_user(self, full_name, email, password):
        """Create a new user"""
        try:
            # Validate email format
            if not self.validate_email(email):
                return False, "Invalid email format"
            
            # Validate password
            is_valid_password, password_message = self.validate_password(password)
            if not is_valid_password:
                return False, password_message
            
            # Check if user already exists
            if self.user_exists(email):
                return False, "User already exists with this email"
            
            # Hash password
            hashed_password = self.hash_password(password)
            
            # Create user document
            user_doc = {
                "full_name": full_name,
                "email": email.lower(),
                "password": hashed_password,
                "created_at": datetime.utcnow(),
                "last_login": None,
                "is_active": True
            }
            
            # Insert user into database
            result = self.users_collection.insert_one(user_doc)
            
            if result.inserted_id:
                return True, "User created successfully"
            else:
                return False, "Failed to create user"
                
        except Exception as e:
            print(f"Error creating user: {e}")
            return False, "An error occurred while creating the user"
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        try:
            # Find user by email
            user = self.users_collection.find_one({"email": email.lower()})
            
            if not user:
                return False, "Invalid email or password", None
            
            # Check if user is active
            if not user.get('is_active', True):
                return False, "Account is deactivated", None
            
            # Verify password
            if self.verify_password(password, user['password']):
                # Update last login time
                self.users_collection.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"last_login": datetime.utcnow()}}
                )
                
                # Return user data without password
                user_data = {
                    "id": str(user["_id"]),
                    "full_name": user["full_name"],
                    "email": user["email"],
                    "created_at": user["created_at"],
                    "last_login": datetime.utcnow()
                }
                
                return True, "Login successful", user_data
            else:
                return False, "Invalid email or password", None
                
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return False, "An error occurred during authentication", None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            user = self.users_collection.find_one({"_id": ObjectId(user_id)})
            if user:
                return {
                    "id": str(user["_id"]),
                    "full_name": user["full_name"],
                    "email": user["email"],
                    "created_at": user["created_at"],
                    "last_login": user.get("last_login")
                }
            return None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    def update_user_profile(self, user_id, full_name=None, email=None):
        """Update user profile"""
        try:
            update_data = {}
            if full_name:
                update_data["full_name"] = full_name
            if email:
                if not self.validate_email(email):
                    return False, "Invalid email format"
                # Check if email is already taken by another user
                existing_user = self.users_collection.find_one({
                    "email": email.lower(),
                    "_id": {"$ne": ObjectId(user_id)}
                })
                if existing_user:
                    return False, "Email is already taken"
                update_data["email"] = email.lower()
            
            if update_data:
                result = self.users_collection.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": update_data}
                )
                if result.modified_count > 0:
                    return True, "Profile updated successfully"
                else:
                    return False, "No changes made"
            else:
                return False, "No data to update"
                
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return False, "An error occurred while updating profile"

# Singleton instance
auth_service = AuthService()
