namespace SimulacaoProvas.Application.DTOs
{
    public class UsuarioCadastroDTO
    {
    public required string Email { get; set; }
    public required string Nome { get; set; }
    public required string Senha { get; set; }
    public string ProvedorAutenticacao { get; set; } = "local";
    public string? Foto { get; set; }
    }
}
