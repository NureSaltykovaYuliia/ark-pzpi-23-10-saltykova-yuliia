using System.ComponentModel.DataAnnotations;

namespace Application.DTOs
{
    public class CreateUpdateDogDto
    {
        [Required(ErrorMessage = "Ім'я собаки обов'язкове")]
        public string Name { get; set; }

        public string Breed { get; set; }

        public DateTime DateOfBirth { get; set; }

        public string Description { get; set; }
    }
}
