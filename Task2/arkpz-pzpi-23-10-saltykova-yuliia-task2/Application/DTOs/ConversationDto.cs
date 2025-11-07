namespace Application.DTOs
{
    public class ConversationDto
    {
        public int Id { get; set; }
        public string? Name { get; set; }
        public List<int> ParticipantIds { get; set; } = new List<int>();
        public List<string> ParticipantNames { get; set; } = new List<string>();
    }
}
