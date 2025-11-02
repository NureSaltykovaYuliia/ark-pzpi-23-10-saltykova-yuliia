using Microsoft.VisualBasic;
using System;

namespace Entities.Models
{
    public class Message
    {
        public int Id { get; set; }
        public string Content { get; set; } 
        public DateTime Timestamp { get; set; } = DateTime.UtcNow; 

        // Зв'язок: Хто відправив? (Один-до-багатьох)
        public int SenderId { get; set; }
        public User Sender { get; set; }

        // Зв'язок: До якої розмови належить? (Один-до-багатьох)
        public int ConversationId { get; set; }
        public Conversation Conversation { get; set; }
    }
}