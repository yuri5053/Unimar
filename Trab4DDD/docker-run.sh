
echo "🐳 Comando do Professor Victor Para Facilitar Docker Run"
echo "📚 Demonstração de Clean Architecture + SOLID + Design Patterns + DDD"

mkdir -p data

echo "🔨 Alunos - Montando a build da imagem Docker..."
docker build -t biblioteca-api:latest .

if [ $? -eq 0 ]; then
    echo "✅ Build concluído com sucesso!"
    
    echo "🚀 Iniciando container..."
    docker-compose -f docker-compose.dev.yml up -d
    
    if [ $? -eq 0 ]; then
        echo "✅ Container iniciado com sucesso!"
        echo ""
        echo "🌐 API disponível em: http://localhost:5001"
        echo "📖 Documentação: http://localhost:5001/api/docs"
        echo "💚 Health check: http://localhost:5001/api/biblioteca/health"
        echo ""
        echo "📋 Comandos úteis:"
        echo "  - Ver logs: docker-compose -f docker-compose.dev.yml logs -f"
        echo "  - Parar: docker-compose -f docker-compose.dev.yml down"
        echo "  - Rebuild: docker-compose -f docker-compose.dev.yml up --build -d"
        echo ""
        echo "🧪 Teste rápido:"
        echo "  curl http://localhost:5001/api/biblioteca/health"
    else
        echo "❌ Erro ao iniciar container"
        exit 1
    fi
else
    echo "❌ Erro no build da imagem"
    exit 1
fi

