from fastapi import APIRouter, HTTPException, Depends
from models import UserRegister, UserResponse
from database import Database
import uuid

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register")
async def register(user_data: UserRegister):
    """
    Enregistrer un nouvel utilisateur avec magic link.
    MVP: on retourne juste l'ID de session pour tester.
    """
    try:
        # Vérifier si l'utilisateur existe déjà
        existing_user = Database.get_user_by_email(user_data.email)
        if existing_user:
            return {
                "user_id": existing_user["id"],
                "email": existing_user["email"],
                "message": "User already registered"
            }
        
        # Créer le nouvel utilisateur
        new_user = Database.create_user(
            email=user_data.email,
            freelance_type=user_data.freelance_type,
            years_experience=user_data.years_experience
        )
        
        if not new_user:
            raise HTTPException(status_code=500, detail="Failed to create user")
        
        return {
            "user_id": new_user["id"],
            "email": new_user["email"],
            "freelance_type": new_user["freelance_type"],
            "message": "User registered successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{user_id}")
async def get_user(user_id: str):
    """Récupérer les infos d'un utilisateur"""
    try:
        user = Database.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse(**user)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(email: str):
    """
    MVP magic link stub: retourner l'utilisateur s'il existe.
    En production, envoyer un email avec lien sécurisé.
    """
    try:
        user = Database.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found. Register first.")
        
        return {
            "user_id": user["id"],
            "email": user["email"],
            "message": "Login successful"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
