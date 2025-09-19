namespace SimulacaoProvas.Application.DTOs
{
    public class UsuarioRespostaDTO
    {
    public required string Email { get; set; }
    public required string Nome { get; set; }
    public string? Foto { get; set; }
    public required string Token { get; set; }
    }
}
