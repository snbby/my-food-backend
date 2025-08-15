import React, { useEffect, useState } from 'react';
import './table.css'

interface Product {
  id: number;
  product_name: string;
  brands: string;
  countries: string;
  carbohydrates_100g: number;
	proteins_100g: number;      
	fat_100g: number;
}

const App: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    fetch('/api/foodproducts/search/?limit=30')
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h1>My-food</h1>
      <table>
        <thead>
          <tr>
            <th>Product Name</th>
            <th>Brands</th>
            <th>Country</th>
            <th>Carbohydrates</th>
            <th>Proteins</th>
            <th>Fat</th>
          </tr>
        </thead>
        <tbody>
          {products.map((p) => (
            <tr key={p.id}>
              <td>{p.product_name}</td>
              <td>{p.brands}</td>
              <td>{p.countries}</td>
              <td>{p.carbohydrates_100g}</td>
              <td>{p.proteins_100g}</td>
              <td>{p.fat_100g}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;
