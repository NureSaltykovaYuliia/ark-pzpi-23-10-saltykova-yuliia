using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace Entities.Models
{
    public class User
    {
        public int Id { get; set; }
        public string Username { get; set; }
        public string Email { get; set; }
        public string PasswordHash { get; set; }
        public string Bio { get; set; }
        public UserRole Role { get; set; }

        // Геолокація для пошуку компаньйонів (координати адреси користувача)
        public double? LastLatitude { get; set; }
        public double? LastLongitude { get; set; }

        // Активність та безпека
        public DateTime? LastActivity { get; set; } // Остання активність користувача
        public bool IsBlocked { get; set; } = false; // Блокування адміністратором
        public string? BlockReason { get; set; } // Причина блокування

        // Навігаційні властивості (зв'язки)
        public ICollection<Dog> Dogs { get; set; } = new List<Dog>(); // Мої собаки
        public ICollection<User> Friends { get; set; } = new List<User>(); // Мої друзі
        public ICollection<Event> Events { get; set; } = new List<Event>(); // Події, в яких я беру участь
        public ICollection<Event> OrganizedEvents { get; set; } = new List<Event>(); // Події, які я організував

        // Разговоры, в которых я участвую
        public ICollection<Conversation> Conversations { get; set; } = new List<Conversation>();

        // Сообщения, которые я отправил
        public ICollection<Message> SentMessages { get; set; } = new List<Message>();

        // Уведомления пользователя
        public ICollection<Notification> Notifications { get; set; } = new List<Notification>();
    }
}
