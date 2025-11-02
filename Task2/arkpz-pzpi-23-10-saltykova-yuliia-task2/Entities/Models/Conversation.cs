using System.Collections.Generic;

namespace Entities.Models
{
    public class Conversation
    {
        public int Id { get; set; }
        public string? Name { get; set; } 

        // Зв'язок: Хто бере участь? (Багато-до-багатьох)
        public ICollection<User> Participants { get; set; } = new List<User>();

        // Зв'язок: Які повідомлення в цьому чаті? (Один-до-багатьох)
        public ICollection<Message> Messages { get; set; } = new List<Message>();
    }
}