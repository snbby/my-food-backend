package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"

	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type FoodProduct struct {
	ID                *int     `json:"id" gorm:"column:id"`
	CreatedAt         *string  `json:"created_at" gorm:"column:created_at"`
	UpdatedAt         *string  `json:"updated_at" gorm:"column:updated_at"`
	ProductName       *string  `json:"product_name" gorm:"column:product_name"`
	Brands            *string  `json:"brands" gorm:"column:brands"`
	Countries         *string  `json:"countries" gorm:"column:countries"`
	Carbohydrates100g *float64 `json:"carbohydrates_100g" gorm:"column:carbohydrates_100g"`
	Proteins100g      *float64 `json:"proteins_100g" gorm:"column:proteins_100g"`
	Fat100g           *float64 `json:"fat_100g" gorm:"column:fat_100g"`
}

func (FoodProduct) TableName() string { return "myfood_foodproduct" }

var db *gorm.DB

func initDB() {
	host := os.Getenv("MYFOOD_DATABASE_HOST")
	port := os.Getenv("MYFOOD_DATABASE_PORT")
	name := os.Getenv("MYFOOD_DATABASE_NAME")
	user := os.Getenv("MYFOOD_DATABASE_USER")
	pass := os.Getenv("MYFOOD_DATABASE_PASS")

	dsn := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable", host, port, user, pass, name)
	var err error
	db, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatalf("failed to connect database: %v", err)
	}
}

// @Summary List food products
// @Param q query string false "Product name contains"
// @Param limit query int false "Limit" default(30)
// @Param offset query int false "Offset" default(0)
// @Produce json
// @Success 200 {array} FoodProduct
// @Router /api/foodproducts/search/ [get]
func getProducts(c *gin.Context) {
	q := c.Query("q")
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "30"))
	if limit < 1 {
		limit = 1
	}
	if limit > 100 {
		limit = 100
	}
	offset, _ := strconv.Atoi(c.DefaultQuery("offset", "0"))
	if offset < 0 {
		offset = 0
	}

	query := db.Model(&FoodProduct{})
	if q != "" {
		query = query.Where("product_name ILIKE ?", "%"+q+"%")
	}
	var items []FoodProduct
	if err := query.Offset(offset).Limit(limit).Find(&items).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"detail": err.Error()})
		return
	}
	c.JSON(http.StatusOK, items)
}

func main() {
	initDB()
	r := gin.Default()
	r.GET("/api/foodproducts/search/", getProducts)
	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))
	if err := r.Run(":8002"); err != nil {
		log.Fatal(err)
	}
}
