import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from domain.entities.livro import Livro
    from domain.entities.usuario import Usuario
    from domain.value_objects.isbn import ISBN
    from domain.value_objects.email import Email

    print("✅ Importações do domínio funcionando")

    # Teste de criação de entidades
    isbn = ISBN("978-0134494166")
    livro = Livro(titulo="Clean Architecture", autor="Robert Martin", isbn=isbn)
    print(f"✅ Livro criado: {livro.titulo}")

    email = Email("teste@email.com")
    usuario = Usuario(nome="João Silva", email=email)
    print(f"✅ Usuário criado: {usuario.nome}")

    # Teste de comportamentos
    livro.emprestar()
    print(f"✅ Livro emprestado: disponível = {livro.disponivel}")

    livro.devolver()
    print(f"✅ Livro devolvido: disponível = {livro.disponivel}")

    print("🎉 Estrutura DDD funcionando corretamente!")

except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback

    traceback.print_exc()