namespace SimulacaoProvas.API.DTOs
{
    public class RespostaUsuarioQuestaoDTO
    {
        public int Id { get; set; }
        public int UsuarioId { get; set; }
        public int QuestaoId { get; set; }
        public string OpcaoSelecionada { get; set; } = string.Empty;
        public bool EstaCorreta { get; set; }
        public DateTime RespondidoEm { get; set; }
    }
}
