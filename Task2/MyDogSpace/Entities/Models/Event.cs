using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Models
{
    public class Event
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public DateTime StartTime { get; set; }
        public DateTime EndTime { get; set; }
        public EventType Type { get; set; }

        // Геолокація події
        public double Latitude { get; set; }
        public double Longitude { get; set; }

        // Зв'язок "один-до-багатьох": у події є один організатор
        public int OrganizerId { get; set; }
        public User Organizer { get; set; }

        // Зв'язок "багато-до-багатьох": у події багато учасників
        public ICollection<User> Participants { get; set; } = new List<User>();
    }
}
