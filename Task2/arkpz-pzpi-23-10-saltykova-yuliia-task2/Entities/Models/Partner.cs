using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Models
{
    public class Partner
    {
        public int Id { get; set; }
        public string Name { get; set; } // Назва клініки, магазину
        public string Description { get; set; }
        public string Address { get; set; } 
        public string PhoneNumber { get; set; }
        public string Website { get; set; }

        
        public double Latitude { get; set; }
        public double Longitude { get; set; }
    }
}
