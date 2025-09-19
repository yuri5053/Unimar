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
    public class MateriaController : ControllerBase
    {
    private readonly SimulacaoProvasDbContext _context;
    private readonly Microsoft.Extensions.Caching.Memory.IMemoryCache _cache;
    private readonly ILogger<MateriaController> _logger;

        public MateriaController(SimulacaoProvasDbContext context, Microsoft.Extensions.Caching.Memory.IMemoryCache cache, ILogger<MateriaController> logger)
        {
            _context = context;
            _cache = cache;
            _logger = logger;
        }

        [HttpGet("{id}/questoes")]
        public async Task<IActionResult> ListarQuestoes(int id)
        {
            var materia = await _context.Materias
                .Include(m => m.Questoes)
                .FirstOrDefaultAsync(m => m.Id == id);

            if (materia == null)
            {
                return NotFound("Matéria não encontrada.");
            }

            return Ok(materia.Questoes);
        }

        [HttpGet]
        public async Task<IActionResult> Listar()
        {
            _logger.LogInformation("Listando matérias");
            if (!_cache.TryGetValue("materias", out object? materiasObj) || materiasObj is not List<Materia> materiasTmpNullable)
            {
                var materias = await _context.Materias.AsNoTracking().ToListAsync();
                _cache.Set("materias", materias, new MemoryCacheEntryOptions
                {
                    AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
                });
                return Ok(materias);
            }
            return Ok(materiasTmpNullable!);
        }

        [HttpPost]
        public async Task<IActionResult> Criar([FromBody] Materia materia)
        {
            _logger.LogInformation("Criando matéria: {Nome}", materia.Nome);
            if (string.IsNullOrWhiteSpace(materia.Nome))
            {
                _logger.LogWarning("Tentativa de criar matéria sem nome");
                return BadRequest("Nome da matéria é obrigatório.");
            }
            _context.Materias.Add(materia);
            await _context.SaveChangesAsync();
            _logger.LogInformation("Matéria criada com sucesso: {Id}", materia.Id);
            return CreatedAtAction(nameof(ObterPorId), new { id = materia.Id }, materia);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> ObterPorId(int id)
        {
            _logger.LogInformation("Buscando matéria por id: {Id}", id);
            var materia = await _context.Materias.FindAsync(id);
            if (materia == null)
            {
                _logger.LogWarning("Matéria não encontrada: {Id}", id);
                return NotFound();
            }
            return Ok(materia);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Atualizar(int id, [FromBody] Materia materia)
        {
            _logger.LogInformation("Atualizando matéria: {Id}", id);
            if (id != materia.Id)
            {
                _logger.LogWarning("Id da URL não bate com o do corpo da requisição");
                return BadRequest();
            }
            var existe = await _context.Materias.AnyAsync(m => m.Id == id);
            if (!existe)
            {
                _logger.LogWarning("Matéria para atualizar não encontrada: {Id}", id);
                return NotFound();
            }
            _context.Entry(materia).State = EntityState.Modified;
            await _context.SaveChangesAsync();
            _logger.LogInformation("Matéria atualizada: {Id}", id);
            return NoContent();
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> Remover(int id)
        {
            _logger.LogInformation("Removendo matéria: {Id}", id);
            var materia = await _context.Materias.FindAsync(id);
            if (materia == null)
            {
                _logger.LogWarning("Matéria para remover não encontrada: {Id}", id);
                return NotFound();
            }
            _context.Materias.Remove(materia);
            await _context.SaveChangesAsync();
            _logger.LogInformation("Matéria removida: {Id}", id);
            return NoContent();
        }
    }
}
