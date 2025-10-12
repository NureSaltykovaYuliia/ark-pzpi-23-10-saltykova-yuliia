using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Models
{
    public class Dog
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Breed { get; set; } // Порода
        public string Description { get; set; }
        public DateTime DateOfBirth { get; set; }
        public string PhotoUrl { get; set; } 

        // Зв'язок "один-до-багатьох": у собаки є один власник
        public int OwnerId { get; set; }
        public User Owner { get; set; }

        // Зв'язок "один-до-одного" з розумним пристроєм
        public SmartDevice SmartDevice { get; set; }
    }
}
