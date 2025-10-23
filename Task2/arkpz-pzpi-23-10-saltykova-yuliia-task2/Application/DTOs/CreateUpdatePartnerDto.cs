using System.ComponentModel.DataAnnotations;

namespace Application.DTOs
{
    public class CreateUpdatePartnerDto
    {
        [Required(ErrorMessage = "Назва партнера обов'язкова")]
        public string Name { get; set; }

        public string Description { get; set; }

        [Required(ErrorMessage = "Адреса обов'язкова")]
        public string Address { get; set; }

        public string PhoneNumber { get; set; }

        public string Website { get; set; }

        public double Latitude { get; set; }

        public double Longitude { get; set; }
    }
}
