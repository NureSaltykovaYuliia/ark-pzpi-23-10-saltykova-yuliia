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

        // Геолокація для пошуку компаньйонів
        public double? LastLatitude { get; set; }
        public double? LastLongitude { get; set; }

        // Навігаційні властивості (зв'язки)
        public ICollection<Dog> Dogs { get; set; } = new List<Dog>(); // Мої собаки
        public ICollection<User> Friends { get; set; } = new List<User>(); // Мої друзі
        public ICollection<Event> Events { get; set; } = new List<Event>(); // Події, в яких я беру участь
        public ICollection<Event> OrganizedEvents { get; set; } = new List<Event>(); // Події, які я організував
    }
}
