using Microsoft.Extensions.Caching.Memory;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SimulacaoProvas.Infrastructure.Data;
using System.Security.Claims;

namespace SimulacaoProvas.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class EstatisticasController : ControllerBase
    {
    private readonly SimulacaoProvasDbContext _context;
    private readonly IMemoryCache _cache;
    private readonly ILogger<EstatisticasController> _logger;

        public EstatisticasController(SimulacaoProvasDbContext context, IMemoryCache cache, ILogger<EstatisticasController> logger)
        {
            _context = context;
            _cache = cache;
            _logger = logger;
        }

        [HttpGet]
        public async Task<IActionResult> GetEstatisticas()
        {
            _logger.LogInformation("Obtendo estatísticas do usuário logado");
            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier) ?? User.FindFirstValue(ClaimTypes.Name) ?? User.FindFirstValue(ClaimTypes.Email);
            if (string.IsNullOrEmpty(userId))
            {
                _logger.LogWarning("Usuário não autenticado ao obter estatísticas");
                return Unauthorized();
            }
            if (!int.TryParse(userId, out var usuarioIdInt))
            {
                _logger.LogWarning("Id do usuário inválido ao obter estatísticas");
                return Unauthorized();
            }
            return await GetEstatisticasPorUsuario(usuarioIdInt);
        }

        [HttpGet("todos")]
        public async Task<IActionResult> GetEstatisticasTodosUsuarios()
        {
            _logger.LogInformation("Obtendo estatísticas de todos os usuários");
            var usuarios = await _context.RespostasUsuarioQuestao
                .GroupBy(r => r.UsuarioId)
                .Select(g => new {
                    usuarioId = g.Key,
                    total = g.Count(),
                    acertos = g.Count(r => r.EstaCorreta),
                    erros = g.Count() - g.Count(r => r.EstaCorreta),
                    percentualAcerto = g.Count() > 0 ? (g.Count(r => r.EstaCorreta) * 100.0 / g.Count()) : 0
                })
                .ToListAsync();
            return Ok(usuarios);
        }

        [HttpGet("usuario/{id}")]
        public async Task<IActionResult> GetEstatisticasPorId(int id)
        {
            _logger.LogInformation("Obtendo estatísticas do usuário por id: {Id}", id);
            return await GetEstatisticasPorUsuario(id);
        }

        private async Task<IActionResult> GetEstatisticasPorUsuario(int usuarioId)
        {
            string cacheKey = $"estatisticas_usuario_{usuarioId}";
            if (!_cache.TryGetValue(cacheKey, out object? estatisticasObj) || estatisticasObj is not object estatisticasTmpNullable)
            {
                var total = await _context.RespostasUsuarioQuestao.CountAsync(r => r.UsuarioId == usuarioId);
                var acertos = await _context.RespostasUsuarioQuestao.CountAsync(r => r.UsuarioId == usuarioId && r.EstaCorreta);
                var erros = total - acertos;
                var estatisticas = new { total, acertos, erros, percentualAcerto = total > 0 ? (acertos * 100.0 / total) : 0 };
                _cache.Set(cacheKey, estatisticas, new MemoryCacheEntryOptions
                {
                    AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
                });
                _logger.LogInformation("Estatísticas calculadas para usuário {UsuarioId}", usuarioId);
                return Ok(estatisticas);
            }
            _logger.LogInformation("Estatísticas recuperadas do cache para usuário {UsuarioId}", usuarioId);
            return Ok(estatisticasObj);
        }
    }
}
