using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Models
{
     public class SmartDevice
    {
        public int Id { get; set; } 
        public string DeviceGuid { get; set; } 
        public double LastLatitude { get; set; }
        public double LastLongitude { get; set; }
        public double BatteryLevel { get; set; } 

        // Зв'язок "один-до-одного": пристрій прив'язаний до однієї собаки
        public int DogId { get; set; }
        public Dog Dog { get; set; }
    }
}
