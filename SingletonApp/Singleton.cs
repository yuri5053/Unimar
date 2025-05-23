using System;

namespace SingletonApp
{
    // A classe sealed impede que seja herdada
    public sealed class Singleton
    {
        // Objeto para sincronização em cenários com várias threads
        private static readonly object _syncLock = new object();
        // Armazena a instancia unica da classe
        private static Singleton _instance = null;

        // Uma propriedade exemplo para armazenar um valor
        public string Value { get; private set; }

        // Flag para garantir que a inicialização ocorra somente uma vez
        private bool _initialized = false;

        private Singleton() { }

        static void Main(string[] args)
        {
            Console.WriteLine("Projeto Singleton compilado com sucesso!");         
            var instance = Singleton.GetInstance();
            instance.Initialize("Valor Inicial");
            Console.WriteLine("Valor do Singleton: " + instance.Value);
        }

        // Metodo publico para obter a instancia unica
        public static Singleton GetInstance()
        {
            if (_instance == null)
            {
                lock (_syncLock)
                {
                    if (_instance == null)
                    {
                        _instance = new Singleton();
                    }
                }
            }
            return _instance;
        }

        // Faz com que só seja possivel chamar a instancia uma unica vez (a segunda em diante vai ser ignorada)
        public void Initialize(string value)
        {
            if (!_initialized)
            {
                Value = value;
                _initialized = true;
            }
        }
    }
}
