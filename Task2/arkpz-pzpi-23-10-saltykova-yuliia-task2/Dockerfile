# Етап збірки (Build stage)
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# 1. Копіюємо файл рішення (.sln) та файли проектів (.csproj)
# Зверни увагу: згідно зі скріншотом 5, .sln знаходиться всередині папки MyDogSpace
COPY ["MyDogSpace/MyDogSpace.sln", "MyDogSpace/"]
COPY ["MyDogSpace/MyDogSpace.csproj", "MyDogSpace/"]
COPY ["Application/Application.csproj", "Application/"]
COPY ["Infrastructure/Infrastructure.csproj", "Infrastructure/"]
COPY ["Entities/Entities.csproj", "Entities/"]

# 2. Відновлюємо залежності
RUN dotnet restore "MyDogSpace/MyDogSpace.sln"

# 3. Копіюємо весь інший вихідний код
COPY . .

# 4. Збираємо проект
WORKDIR "/src/MyDogSpace"
RUN dotnet build "MyDogSpace.csproj" -c Release -o /app/build

# Етап публікації (Publish stage)
FROM build AS publish
RUN dotnet publish "MyDogSpace.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Етап запуску (Runtime stage)
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app

# Встановлюємо curl для healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Створюємо папку для бази даних з правильними правами
RUN mkdir -p /app/data && chmod 777 /app/data

# Копіюємо опубліковані файли з етапу publish
COPY --from=publish /app/publish .

# Відкриваємо порт (тільки HTTP, HTTPS налаштовується окремо)
EXPOSE 8080

# Налаштування змінних середовища
ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production

# Точка входу (запуск головного dll файлу)
ENTRYPOINT ["dotnet", "MyDogSpace.dll"]