using System.ComponentModel.DataAnnotations;

namespace Application.DTOs
{
    public class CreateUpdateEventDto
    {
        [Required(ErrorMessage = "Назва події обов'язкова")]
        public string Name { get; set; }

        public string Description { get; set; }

        public DateTime StartTime { get; set; }

        public DateTime EndTime { get; set; }

        public EventType Type { get; set; }

        public double Latitude { get; set; }

        public double Longitude { get; set; }
    }
}
