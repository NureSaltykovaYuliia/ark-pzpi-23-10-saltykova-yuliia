using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Entities.Models;

namespace Infrastructure
{
    public class MyDbContext : DbContext
    {
        
        public MyDbContext(DbContextOptions<MyDbContext> options) : base(options) { }

        public DbSet<User> Users { get; set; }
        public DbSet<Dog> Dogs { get; set; }
        public DbSet<Event> Events { get; set; }
        public DbSet<Partner> Partners { get; set; }
        public DbSet<SmartDevice> SmartDevices { get; set; }

       
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

           
            modelBuilder.Entity<User>()
                .HasMany(u => u.Events)
                .WithMany(e => e.Participants);

            modelBuilder.Entity<User>()
                .HasMany(u => u.Friends)
                .WithMany(); 

            modelBuilder.Entity<Event>()
                .HasOne(e => e.Organizer)
                .WithMany(u => u.OrganizedEvents)
                .HasForeignKey(e => e.OrganizerId)
                .OnDelete(DeleteBehavior.Restrict); 

            modelBuilder.Entity<Dog>()
                .HasOne(d => d.Owner)
                .WithMany(u => u.Dogs)
                .HasForeignKey(d => d.OwnerId);

            modelBuilder.Entity<Dog>()
                .HasOne(d => d.SmartDevice)
                .WithOne(sd => sd.Dog)
                .HasForeignKey<SmartDevice>(sd => sd.DogId);
        }
    }
}
