# Teste simples da API

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from src.domain.entities import Livro, Usuario, Emprestimo
    from src.domain.value_objects.isbn import ISBN
    from src.domain.value_objects.email import Email
    print("✅ Importações do domínio funcionando")
    
    # Teste de criação de entidades
    isbn = ISBN("978-0134494166")
    livro = Livro("", "Clean Architecture", "Robert Martin", isbn)
    print(f"✅ Livro criado: {livro.titulo}")
    
    email = Email("teste@email.com")
    usuario = Usuario("", "João Silva", email)
    print(f"✅ Usuário criado: {usuario.nome}")
    
    print("🎉 Estrutura DDD funcionando corretamente!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

