from tokenize import Token
import skill.dairy_api as dairy_api

Token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbiI6InRhbnVzaGFfdkBpbmJveC5ydSIsInBhc3N3b3JkIjoidmQzNzQ3NTA3IiwidHlwZSI6ImVtYWlsIiwidGltZSI6MTY1OTk2ODEyN30.l15uURPQTSTtlQw4LCXAxOWwwZZqO6Ghh0Tl5oLjbj8"


def test_get_students():
    students = dairy_api.get_students(Token)
    
