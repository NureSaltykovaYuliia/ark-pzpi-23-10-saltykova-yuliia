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
        public DbSet<Conversation> Conversations { get; set; }
        public DbSet<Message> Messages { get; set; }
        public DbSet<AdminCode> AdminCodes { get; set; }
        public DbSet<Notification> Notifications { get; set; }


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

            // Dog → User (видалення користувача → видалення його собак)
            modelBuilder.Entity<Dog>()
                .HasOne(d => d.Owner)
                .WithMany(u => u.Dogs)
                .HasForeignKey(d => d.OwnerId)
                .OnDelete(DeleteBehavior.Cascade);

            // Dog ↔ SmartDevice (видалення собаки → видалення пристрою)
            modelBuilder.Entity<Dog>()
                .HasOne(d => d.SmartDevice)
                .WithOne(sd => sd.Dog)
                .HasForeignKey<SmartDevice>(sd => sd.DogId)
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<AdminCode>()
                .HasOne(ac => ac.UsedBy)
                .WithMany()
                .HasForeignKey(ac => ac.UsedByUserId)
                .OnDelete(DeleteBehavior.Cascade);

            // Message → Conversation (видалення розмови → видалення всіх повідомлень)
            modelBuilder.Entity<Message>()
                .HasOne(m => m.Conversation)
                .WithMany(c => c.Messages)
                .HasForeignKey(m => m.ConversationId)
                .OnDelete(DeleteBehavior.Cascade);

            // Message → Sender (НЕ можна видалити користувача, якщо є його повідомлення)
            modelBuilder.Entity<Message>()
                .HasOne(m => m.Sender)
                .WithMany(u => u.SentMessages)
                .HasForeignKey(m => m.SenderId)
                .OnDelete(DeleteBehavior.Restrict);

            // Conversation ↔ User (Many-to-Many) - учасники розмови
            modelBuilder.Entity<Conversation>()
                .HasMany(c => c.Participants)
                .WithMany(u => u.Conversations);

            // Notification → User (видалення користувача → видалення його уведомлений)
            modelBuilder.Entity<Notification>()
                .HasOne(n => n.User)
                .WithMany(u => u.Notifications)
                .HasForeignKey(n => n.UserId)
                .OnDelete(DeleteBehavior.Cascade);
        }
    }
}
