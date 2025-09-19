using Microsoft.Extensions.Caching.Memory;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SimulacaoProvas.Domain.Entities;
using SimulacaoProvas.Infrastructure.Data;

namespace SimulacaoProvas.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class QuestaoController : ControllerBase
    {
    private readonly SimulacaoProvasDbContext _context;
    private readonly IMemoryCache _cache;
    private readonly ILogger<QuestaoController> _logger;

        public QuestaoController(SimulacaoProvasDbContext context, IMemoryCache cache, ILogger<QuestaoController> logger)
        {
            _context = context;
            _cache = cache;
            _logger = logger;
        }

        [HttpGet]
        public async Task<IActionResult> Listar()
        {
            _logger.LogInformation("Listando questões");
            if (!_cache.TryGetValue("questoes", out object? questoesObj) || questoesObj is not List<Questao> questoesTmpNullable)
            {
                var questoes = await _context.Questoes.AsNoTracking().ToListAsync();
                _cache.Set("questoes", questoes, new MemoryCacheEntryOptions
                {
                    AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
                });
                return Ok(questoes);
            }
            return Ok(questoesTmpNullable);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> ObterPorId(int id)
        {
            _logger.LogInformation("Buscando questão por id: {Id}", id);
            var questao = await _context.Questoes.FindAsync(id);
            if (questao == null)
            {
                _logger.LogWarning("Questão não encontrada: {Id}", id);
                return NotFound();
            }
            return Ok(questao);
        }

        [HttpPost]
        public async Task<IActionResult> Criar([FromBody] Questao questao)
        {
            _logger.LogInformation("Criando questão: {Enunciado}", questao.Enunciado);
            if (string.IsNullOrWhiteSpace(questao.Enunciado) || string.IsNullOrWhiteSpace(questao.OpcoesJson) || string.IsNullOrWhiteSpace(questao.OpcaoCorreta))
            {
                _logger.LogWarning("Tentativa de criar questão com campos obrigatórios faltando");
                return BadRequest("Campos obrigatórios não preenchidos.");
            }
            questao.CriadoEm = DateTime.UtcNow;
            _context.Questoes.Add(questao);
            await _context.SaveChangesAsync();
            _logger.LogInformation("Questão criada com sucesso: {Id}", questao.Id);
            return CreatedAtAction(nameof(ObterPorId), new { id = questao.Id }, questao);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Atualizar(int id, [FromBody] Questao questao)
        {
            _logger.LogInformation("Atualizando questão: {Id}", id);
            if (id != questao.Id)
            {
                _logger.LogWarning("Id da URL não bate com o do corpo da requisição");
                return BadRequest();
            }
            var existe = await _context.Questoes.AnyAsync(q => q.Id == id);
            if (!existe)
            {
                _logger.LogWarning("Questão para atualizar não encontrada: {Id}", id);
                return NotFound();
            }
            _context.Entry(questao).State = EntityState.Modified;
            await _context.SaveChangesAsync();
            _logger.LogInformation("Questão atualizada: {Id}", id);
            return NoContent();
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> Remover(int id)
        {
            _logger.LogInformation("Removendo questão: {Id}", id);
            var questao = await _context.Questoes.FindAsync(id);
            if (questao == null)
            {
                _logger.LogWarning("Questão para remover não encontrada: {Id}", id);
                return NotFound();
            }
            _context.Questoes.Remove(questao);
            await _context.SaveChangesAsync();
            _logger.LogInformation("Questão removida: {Id}", id);
            return NoContent();
        }
    }
}
