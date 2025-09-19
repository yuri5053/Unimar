using Microsoft.EntityFrameworkCore;
using SimulacaoProvas.Domain.Entities;

namespace SimulacaoProvas.Infrastructure.Data
{
    public class SimulacaoProvasDbContext : DbContext
    {
        public SimulacaoProvasDbContext(DbContextOptions<SimulacaoProvasDbContext> options) : base(options) { }

        public DbSet<Usuario> Usuarios { get; set; }
        public DbSet<Materia> Materias { get; set; }
        public DbSet<Questao> Questoes { get; set; }
        public DbSet<RespostaUsuarioQuestao> RespostasUsuarioQuestao { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<Questao>()
                .ToTable("questoes"); // Nome correto da tabela no banco
        }
    }
}
