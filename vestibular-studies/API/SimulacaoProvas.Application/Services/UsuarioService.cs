using SimulacaoProvas.Application.DTOs;
using SimulacaoProvas.Domain.Entities;
using SimulacaoProvas.Infrastructure.Data;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace SimulacaoProvas.Application.Services
{
    public class UsuarioService
    {
        private readonly SimulacaoProvasDbContext _context;
        private readonly IPasswordHasher<Usuario> _passwordHasher;
        private readonly IConfiguration _configuration;

        public UsuarioService(SimulacaoProvasDbContext context, IPasswordHasher<Usuario> passwordHasher, IConfiguration configuration)
        {
            _context = context;
            _passwordHasher = passwordHasher;
            _configuration = configuration;
        }

        public async Task<UsuarioRespostaDTO?> CadastrarAsync(UsuarioCadastroDTO dto)
        {
            if (await _context.Usuarios.AnyAsync(u => u.Email == dto.Email))
                return null;

            var usuario = new Usuario
            {
                Email = dto.Email,
                Nome = dto.Nome,
                ProvedorAutenticacao = dto.ProvedorAutenticacao,
                Foto = dto.Foto ?? string.Empty,
                CriadoEm = DateTime.UtcNow,
                SenhaHash = string.Empty
            };
            usuario.SenhaHash = _passwordHasher.HashPassword(usuario, dto.Senha);
            _context.Usuarios.Add(usuario);
            await _context.SaveChangesAsync();
            return new UsuarioRespostaDTO
            {
                Email = usuario.Email,
                Nome = usuario.Nome,
                Foto = usuario.Foto,
                Token = GerarToken(usuario)
            };
        }

        public async Task<UsuarioRespostaDTO?> LoginAsync(UsuarioLoginDTO dto)
        {
            var usuario = await _context.Usuarios.FirstOrDefaultAsync(u => u.Email == dto.Email);
            if (usuario == null)
                return null;
            var result = _passwordHasher.VerifyHashedPassword(usuario, usuario.SenhaHash, dto.Senha);
            if (result == PasswordVerificationResult.Failed)
                return null;
            return new UsuarioRespostaDTO
            {
                Email = usuario.Email,
                Nome = usuario.Nome,
                Foto = usuario.Foto,
                Token = GerarToken(usuario)
            };
        }

        private string GerarToken(Usuario usuario)
        {
            var claims = new[]
            {
                new Claim(JwtRegisteredClaimNames.Sub, usuario.Id.ToString()),
                new Claim(JwtRegisteredClaimNames.Email, usuario.Email),
                new Claim("nome", usuario.Nome)
            };
            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_configuration["Jwt:Key"] ?? "chave_super_secreta"));
            var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
            var token = new JwtSecurityToken(
                issuer: _configuration["Jwt:Issuer"] ?? "SimulacaoProvas",
                audience: _configuration["Jwt:Audience"] ?? "SimulacaoProvas",
                claims: claims,
                expires: DateTime.UtcNow.AddHours(2),
                signingCredentials: creds
            );
            return new JwtSecurityTokenHandler().WriteToken(token);
        }
    }
}
