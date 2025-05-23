using Microsoft.VisualStudio.TestTools.UnitTesting;
// Importa o namespace onde est� a classe Singleton.
using SingletonApp;

namespace SingletonTests
{
    [TestClass]
    public class SingletonUnitTest
    {
        [TestMethod]
        public void SingletonBehaviorTest()
        {
            // Pega a Instance do Singleton e inicialia ela com uma string "Valor Inicial"
            var instance1 = Singleton.GetInstance();
            instance1.Initialize("Valor Inicial");

            // Pega a Instance do Singleton e "tenta" inicializar ela com uma string "Outro Valor" (� pra ser ignorado)
            var instance2 = Singleton.GetInstance();
            instance2.Initialize("Outro Valor");

            // Checando se o valor original da primeira Instance se mantem inalterado
            // AreSame = checa se n�o s�o exatamente o mesmo objeto na memoria        
            Assert.AreSame(instance1, instance2, "As inst�ncias devem ser as mesmas.");
            // AreEqual = checa se eles tem o mesmo valor
            Assert.AreEqual("Valor Inicial", instance1.Value, "O valor deve permanecer inalterado.");
            Assert.AreEqual("Valor Inicial", instance2.Value, "O valor deve permanecer inalterado.");
        }
    }
}
