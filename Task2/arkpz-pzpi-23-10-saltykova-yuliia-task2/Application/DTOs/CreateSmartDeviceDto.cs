using System.ComponentModel.DataAnnotations;

namespace Application.DTOs
{
    public class CreateSmartDeviceDto
    {
        [Required(ErrorMessage = "GUID пристрою обов'язковий")]
        public string DeviceGuid { get; set; }

        public int DogId { get; set; }
    }
}
