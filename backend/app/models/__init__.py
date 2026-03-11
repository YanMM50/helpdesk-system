"""
Models — representações das tabelas do banco de dados como classes Python.
Importar todos aqui garante que o SQLAlchemy os detecta ao criar as tabelas.
"""
from app.models.company import Company
from app.models.user import User
from app.models.equipment import Equipment
from app.models.ticket import Ticket, TicketHistory, Attachment
