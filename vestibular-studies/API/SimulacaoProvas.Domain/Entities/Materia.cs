using System;
using System.Collections.Generic;

namespace SimulacaoProvas.Domain.Entities
{
    public class Materia
    {
    public int Id { get; set; } 
    public required string Nome { get; set; }
    public ICollection<Questao> Questoes { get; set; } = new List<Questao>();
    }
}
