# Infrastructure Layer - Repository Implementations

from typing import List, Optional
from src.domain.entities import Livro, Usuario, Emprestimo, Doacao, Horas
from src.domain.repositories import LivroRepository, UsuarioRepository, EmprestimoRepository, DoacaoRepository, HorasRepository
from src.domain.value_objects.isbn import ISBN
from src.domain.value_objects.email import Email
from src.infrastructure.database.models import LivroModel, UsuarioModel, EmprestimoModel, DoacaoModel, HorasModel
from src.models.user import db
from datetime import datetime


class SQLAlchemyLivroRepository(LivroRepository):
    """
    Implementação concreta do LivroRepository usando SQLAlchemy
    Aplicando SOLID: Dependency Inversion Principle - implementação depende da abstração
    Aplicando DDD: Repository Pattern - implementação na infraestrutura
    """
    
    def salvar(self, livro: Livro) -> None:
        """Salva um livro no banco de dados"""
        livro_model = LivroModel.query.filter_by(id=livro.id).first()
        
        if livro_model:
            # Atualizar existente
            livro_model.titulo = livro.titulo
            livro_model.autor = livro.autor
            livro_model.isbn = str(livro.isbn)
            livro_model.disponivel = livro.disponivel
        else:
            # Criar novo
            livro_model = LivroModel(
                id=livro.id,
                titulo=livro.titulo,
                autor=livro.autor,
                isbn=str(livro.isbn),
                disponivel=livro.disponivel
            )
            db.session.add(livro_model)
        
        db.session.commit()
    
    def buscar_por_id(self, id: str) -> Optional[Livro]:
        """Busca livro por ID"""
        livro_model = LivroModel.query.filter_by(id=id).first()
        if not livro_model:
            return None
        
        return self._model_para_entidade(livro_model)
    
    def buscar_por_isbn(self, isbn: str) -> Optional[Livro]:
        """Busca livro por ISBN"""
        livro_model = LivroModel.query.filter_by(isbn=isbn).first()
        if not livro_model:
            return None
        
        return self._model_para_entidade(livro_model)
    
    def buscar_todos(self) -> List[Livro]:
        """Busca todos os livros"""
        livros_model = LivroModel.query.all()
        return [self._model_para_entidade(livro) for livro in livros_model]
    
    def buscar_disponiveis(self) -> List[Livro]:
        """Busca livros disponíveis"""
        livros_model = LivroModel.query.filter_by(disponivel=True).all()
        return [self._model_para_entidade(livro) for livro in livros_model]
    
    def deletar(self, id: str) -> None:
        """Deleta um livro"""
        livro_model = LivroModel.query.filter_by(id=id).first()
        if livro_model:
            db.session.delete(livro_model)
            db.session.commit()
    
    def _model_para_entidade(self, livro_model: LivroModel) -> Livro:
        """Converte model para entidade de domínio"""
        return Livro(
            id=livro_model.id,
            titulo=livro_model.titulo,
            autor=livro_model.autor,
            isbn=ISBN(livro_model.isbn),
            disponivel=livro_model.disponivel
        )


class SQLAlchemyUsuarioRepository(UsuarioRepository):
    """
    Implementação concreta do UsuarioRepository usando SQLAlchemy
    """
    
    def salvar(self, usuario: Usuario) -> None:
        """Salva um usuário no banco de dados"""
        usuario_model = UsuarioModel.query.filter_by(id=usuario.id).first()
        
        if usuario_model:
            # Atualizar existente
            usuario_model.nome = usuario.nome
            usuario_model.email = str(usuario.email)
            usuario_model.ativo = usuario.ativo
        else:
            # Criar novo
            usuario_model = UsuarioModel(
                id=usuario.id,
                nome=usuario.nome,
                email=str(usuario.email),
                ativo=usuario.ativo
            )
            db.session.add(usuario_model)
        
        db.session.commit()
    
    def buscar_por_id(self, id: str) -> Optional[Usuario]:
        """Busca usuário por ID"""
        usuario_model = UsuarioModel.query.filter_by(id=id).first()
        if not usuario_model:
            return None
        
        return self._model_para_entidade(usuario_model)
    
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """Busca usuário por email"""
        usuario_model = UsuarioModel.query.filter_by(email=email).first()
        if not usuario_model:
            return None
        
        return self._model_para_entidade(usuario_model)
    
    def buscar_todos(self) -> List[Usuario]:
        """Busca todos os usuários"""
        usuarios_model = UsuarioModel.query.all()
        return [self._model_para_entidade(usuario) for usuario in usuarios_model]
    
    def deletar(self, id: str) -> None:
        """Deleta um usuário"""
        usuario_model = UsuarioModel.query.filter_by(id=id).first()
        if usuario_model:
            db.session.delete(usuario_model)
            db.session.commit()
    
    def _model_para_entidade(self, usuario_model: UsuarioModel) -> Usuario:
        """Converte model para entidade de domínio"""
        return Usuario(
            id=usuario_model.id,
            nome=usuario_model.nome,
            email=Email(usuario_model.email),
            ativo=usuario_model.ativo
        )


class SQLAlchemyEmprestimoRepository(EmprestimoRepository):
    """
    Implementação concreta do EmprestimoRepository usando SQLAlchemy
    """
    
    def salvar(self, emprestimo: Emprestimo) -> None:
        """Salva um empréstimo no banco de dados"""
        emprestimo_model = EmprestimoModel.query.filter_by(id=emprestimo.id).first()
        
        if emprestimo_model:
            # Atualizar existente
            emprestimo_model.livro_id = emprestimo.livro_id
            emprestimo_model.usuario_id = emprestimo.usuario_id
            emprestimo_model.data_emprestimo = emprestimo.data_emprestimo
            emprestimo_model.data_devolucao_prevista = emprestimo.data_devolucao_prevista
            emprestimo_model.data_devolucao_real = emprestimo.data_devolucao_real
            emprestimo_model.multa = emprestimo.multa
        else:
            # Criar novo
            emprestimo_model = EmprestimoModel(
                id=emprestimo.id,
                livro_id=emprestimo.livro_id,
                usuario_id=emprestimo.usuario_id,
                data_emprestimo=emprestimo.data_emprestimo,
                data_devolucao_prevista=emprestimo.data_devolucao_prevista,
                data_devolucao_real=emprestimo.data_devolucao_real,
                multa=emprestimo.multa
            )
            db.session.add(emprestimo_model)
        
        db.session.commit()
    
    def buscar_por_id(self, id: str) -> Optional[Emprestimo]:
        """Busca empréstimo por ID"""
        emprestimo_model = EmprestimoModel.query.filter_by(id=id).first()
        if not emprestimo_model:
            return None
        
        return self._model_para_entidade(emprestimo_model)
    
    def buscar_por_usuario(self, usuario_id: str) -> List[Emprestimo]:
        """Busca empréstimos de um usuário"""
        emprestimos_model = EmprestimoModel.query.filter_by(usuario_id=usuario_id).all()
        return [self._model_para_entidade(emp) for emp in emprestimos_model]
    
    def buscar_por_livro(self, livro_id: str) -> List[Emprestimo]:
        """Busca empréstimos de um livro"""
        emprestimos_model = EmprestimoModel.query.filter_by(livro_id=livro_id).all()
        return [self._model_para_entidade(emp) for emp in emprestimos_model]
    
    def buscar_ativos(self) -> List[Emprestimo]:
        """Busca empréstimos ativos (não devolvidos)"""
        emprestimos_model = EmprestimoModel.query.filter_by(data_devolucao_real=None).all()
        return [self._model_para_entidade(emp) for emp in emprestimos_model]
    
    def buscar_em_atraso(self) -> List[Emprestimo]:
        """Busca empréstimos em atraso"""
        agora = datetime.now()
        emprestimos_model = EmprestimoModel.query.filter(
            EmprestimoModel.data_devolucao_real.is_(None),
            EmprestimoModel.data_devolucao_prevista < agora
        ).all()
        return [self._model_para_entidade(emp) for emp in emprestimos_model]
    
    def buscar_todos(self) -> List[Emprestimo]:
        """Busca todos os empréstimos"""
        emprestimos_model = EmprestimoModel.query.all()
        return [self._model_para_entidade(emp) for emp in emprestimos_model]
    
    def deletar(self, id: str) -> None:
        """Deleta um empréstimo"""
        emprestimo_model = EmprestimoModel.query.filter_by(id=id).first()
        if emprestimo_model:
            db.session.delete(emprestimo_model)
            db.session.commit()
    
    def _model_para_entidade(self, emprestimo_model: EmprestimoModel) -> Emprestimo:
        """Converte model para entidade de domínio"""
        return Emprestimo(
            id=emprestimo_model.id,
            livro_id=emprestimo_model.livro_id,
            usuario_id=emprestimo_model.usuario_id,
            data_emprestimo=emprestimo_model.data_emprestimo,
            data_devolucao_prevista=emprestimo_model.data_devolucao_prevista,
            data_devolucao_real=emprestimo_model.data_devolucao_real,
            multa=emprestimo_model.multa
        )

class SQLAlchemyDoacaoRepository(DoacaoRepository):
    """
    Implementação concreta do DoacaoRepository usando SQLAlchemy
    """

    def salvar(self, doacao: Doacao) -> None:
        """Salva uma doação no banco de dados"""
        doacao_model = DoacaoModel.query.filter_by(id=doacao.id).first()
        
        if doacao_model:
            # Atualizar existente
            doacao_model.livro_id = doacao.livro_id
            doacao_model.usuario_id = doacao.usuario_id
            doacao_model.data_doacao = doacao.data_doacao
            doacao_model.creditos = doacao.creditos
        else:
            # Criar novo
            doacao_model = DoacaoModel(
                id=doacao.id,
                livro_id=doacao.livro_id,
                usuario_id=doacao.usuario_id,
                data_doacao=doacao.data_doacao,
                creditos=doacao.creditos
            )
            db.session.add(doacao_model)
        
        db.session.commit()
    
    def buscar_por_id(self, id: str) -> Doacao:
        """Busca doação por ID"""
        doacao_model = DoacaoModel.query.filter_by(id=id).first()
        if not doacao_model:
            return None
        
        return self._model_para_entidade(doacao_model)
    
    def buscar_por_usuario(self, usuario_id: str) -> List[Doacao]:
        """Busca doações de um usuário"""
        doacoes_model = DoacaoModel.query.filter_by(usuario_id=usuario_id).all()
        return [self._model_para_entidade(d) for d in doacoes_model]
    
    def buscar_por_livro(self, livro_id: str) -> Doacao:
        """Busca doações de um livro"""
        doacoes_model = DoacaoModel.query.filter_by(livro_id=livro_id).first()
        if not doacoes_model:
            return None
        return self._model_para_entidade(doacoes_model)
    
    def buscar_todos(self) -> List[Doacao]:
        """Busca todas as doações"""
        doacoes_model = DoacaoModel.query.all()
        return [self._model_para_entidade(d) for d in doacoes_model]
    
    def deletar(self, id: str) -> None:
        """Deleta uma doação"""
        doacao_model = DoacaoModel.query.filter_by(id=id).first()
        if doacao_model:
            db.session.delete(doacao_model)
            db.session.commit

class SQLAlchemyHorasRepository(HorasRepository):
    """
    Implementação concreta do HorasRepository usando SQLAlchemy
    """
    def salvar(self, horas: Horas) -> None:
        """Salva horas no banco de dados"""
        horas_model = HorasModel.query.filter_by(id=horas.id).first()
        
        if horas_model:
            # Atualizar existente
            horas_model.usuario_id = horas.usuario_id
            horas_model.horas = horas.horas
            horas_model.data = horas.data
            horas_model.creditos = horas.creditos
        else:
            # Criar novo
            horas_model = HorasModel(
                id=horas.id,
                usuario_id=horas.usuario_id,
                horas=horas.horas,
                data=horas.data,
                creditos=horas.creditos
            )
            db.session.add(horas_model)
        
        db.session.commit()
    
    def buscar_por_id(self, id: str) -> Horas:
        """Busca horas por ID"""
        horas_model = HorasModel.query.filter_by(id=id).first()
        if not horas_model:
            return None
        
        return self._model_para_entidade(horas_model)
    
    def buscar_por_usuario(self, usuario_id: str) -> List[Horas]:
        """Busca horas de um usuário"""
        horas_model = HorasModel.query.filter_by(usuario_id=usuario_id).all()
        return [self._model_para_entidade(h) for h in horas_model]
    
    def buscar_todos(self) -> List[Horas]:
        """Busca todas as horas"""
        horas_model = HorasModel.query.all()
        return [self._model_para_entidade(h) for h in horas_model]
    
    def deletar(self, id: str) -> None:
        """Deleta uma entrada de horas"""
        horas_model = HorasModel.query.filter_by(id=id).first()
        if horas_model:
            db.session.delete(horas_model)
            db.session.commit()
    
    def _model_para_entidade(self, horas_model: HorasModel) -> Horas:
        """Converte model para entidade de domínio"""
        return Horas(
            id=horas_model.id,
            usuario_id=horas_model.usuario_id,
            horas=horas_model.horas,
            data=horas_model.data,
            creditos=horas_model.creditos
        )