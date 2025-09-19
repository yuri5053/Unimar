using Microsoft.Extensions.Caching.Memory;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SimulacaoProvas.Domain.Entities;
using SimulacaoProvas.Infrastructure.Data;
using System.Security.Claims;

namespace SimulacaoProvas.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class RespostaController : ControllerBase
    {
    private readonly SimulacaoProvasDbContext _context;
    private readonly IMemoryCache _cache;
    private readonly ILogger<RespostaController> _logger;

        public RespostaController(SimulacaoProvasDbContext context, IMemoryCache cache, ILogger<RespostaController> logger)
        {
            _context = context;
            _cache = cache;
            _logger = logger;
        }

        [HttpPost]
        public async Task<IActionResult> Responder([FromBody] RespostaUsuarioQuestao resposta)
        {
            _logger.LogInformation("Usuário respondendo questão: {QuestaoId}", resposta.QuestaoId);
            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier) ?? User.FindFirstValue(ClaimTypes.Name) ?? User.FindFirstValue(ClaimTypes.Email);
            if (string.IsNullOrEmpty(userId))
            {
                _logger.LogWarning("Usuário não autenticado ao responder questão");
                return Unauthorized();
            }
            // resposta.Id será auto-incremento
            if (!int.TryParse(userId, out var usuarioIdInt))
            {
                _logger.LogWarning("Id do usuário inválido ao responder questão");
                return Unauthorized();
            }
            resposta.UsuarioId = usuarioIdInt;
            resposta.RespondidoEm = DateTime.UtcNow;
            var questao = await _context.Questoes.FindAsync(resposta.QuestaoId);
            if (questao == null)
            {
                _logger.LogWarning("Questão não encontrada ao responder: {QuestaoId}", resposta.QuestaoId);
                return BadRequest("Questão não encontrada.");
            }
            resposta.EstaCorreta = resposta.OpcaoSelecionada == questao.OpcaoCorreta;
            _context.RespostasUsuarioQuestao.Add(resposta);
            await _context.SaveChangesAsync();
            _logger.LogInformation("Resposta registrada para usuário {UsuarioId} na questão {QuestaoId}", usuarioIdInt, resposta.QuestaoId);
            return Ok(new { resposta.EstaCorreta, resposta.RespondidoEm });
        }

        [HttpGet("usuario")]
        public async Task<IActionResult> ListarRespostasUsuario()
        {
            _logger.LogInformation("Listando respostas do usuário logado");
            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier) ?? User.FindFirstValue(ClaimTypes.Name) ?? User.FindFirstValue(ClaimTypes.Email);
            if (string.IsNullOrEmpty(userId))
            {
                _logger.LogWarning("Usuário não autenticado ao listar respostas");
                return Unauthorized();
            }
            if (!int.TryParse(userId, out var usuarioIdInt))
            {
                _logger.LogWarning("Id do usuário inválido ao listar respostas");
                return Unauthorized();
            }
            string cacheKey = $"respostas_usuario_{usuarioIdInt}";
            if (!_cache.TryGetValue(cacheKey, out object? respostasObj) || respostasObj is not List<DTOs.RespostaUsuarioQuestaoDTO> respostasTmpNullable)
            {
                var respostas = await _context.RespostasUsuarioQuestao
                    .Where(r => r.UsuarioId == usuarioIdInt)
                    .Select(r => new DTOs.RespostaUsuarioQuestaoDTO {
                        Id = r.Id,
                        UsuarioId = r.UsuarioId,
                        QuestaoId = r.QuestaoId,
                        OpcaoSelecionada = r.OpcaoSelecionada,
                        EstaCorreta = r.EstaCorreta,
                        RespondidoEm = r.RespondidoEm
                    })
                    .ToListAsync();
                _cache.Set(cacheKey, respostas, new MemoryCacheEntryOptions
                {
                    AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
                });
                return Ok(respostas);
            }
            return Ok(respostasTmpNullable);
        }
    }
}
