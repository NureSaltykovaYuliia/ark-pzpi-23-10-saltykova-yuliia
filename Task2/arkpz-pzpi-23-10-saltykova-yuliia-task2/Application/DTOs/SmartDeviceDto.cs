namespace Application.DTOs
{
    public class SmartDeviceDto
    {
        public int Id { get; set; }
        public string DeviceGuid { get; set; }
        public double LastLatitude { get; set; }
        public double LastLongitude { get; set; }
        public double BatteryLevel { get; set; }
        public int DogId { get; set; }
        public string DogName { get; set; }
    }
}
