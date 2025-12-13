using System.ComponentModel.DataAnnotations;

namespace Application.DTOs
{
    public class RegisterDeviceDto
    {
        [Required(ErrorMessage = "GUID пристрою обов'язковий")]
        public string DeviceGuid { get; set; }
    }
}
