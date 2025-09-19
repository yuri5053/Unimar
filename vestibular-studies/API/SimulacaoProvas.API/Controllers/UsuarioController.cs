using Microsoft.AspNetCore.Mvc;
using SimulacaoProvas.Application.DTOs;
using SimulacaoProvas.Application.Services;
using Microsoft.AspNetCore.Identity;
using SimulacaoProvas.Domain.Entities;

namespace SimulacaoProvas.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class UsuarioController : ControllerBase
    {
        private readonly UsuarioService _usuarioService;
        private readonly IPasswordHasher<Usuario> _passwordHasher;

        public UsuarioController(UsuarioService usuarioService, IPasswordHasher<Usuario> passwordHasher)
        {
            _usuarioService = usuarioService;
            _passwordHasher = passwordHasher;
        }

        [HttpPost("cadastro")]
        public async Task<IActionResult> Cadastrar([FromBody] UsuarioCadastroDTO dto)
        {
            var resposta = await _usuarioService.CadastrarAsync(dto);
            if (resposta == null)
                return BadRequest("E-mail já cadastrado.");
            return Ok(resposta);
        }

        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] UsuarioLoginDTO dto)
        {
            var resposta = await _usuarioService.LoginAsync(dto);
            if (resposta == null)
                return Unauthorized("E-mail ou senha inválidos.");
            return Ok(resposta);
        }
    }
}
