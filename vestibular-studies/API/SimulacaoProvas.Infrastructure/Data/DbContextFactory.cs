using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;

namespace SimulacaoProvas.Infrastructure.Data
{
    public class DbContextFactory : IDesignTimeDbContextFactory<SimulacaoProvasDbContext>
    {
        public SimulacaoProvasDbContext CreateDbContext(string[] args)
        {
            var optionsBuilder = new DbContextOptionsBuilder<SimulacaoProvasDbContext>();
            optionsBuilder.UseMySql(
                "Server=localhost;Database=simulacaoprovas;User=root;Password=;Port=3306;",
                new MySqlServerVersion(new Version(8, 0, 36)) 
            );
            return new SimulacaoProvasDbContext(optionsBuilder.Options);
        }
    }
}
