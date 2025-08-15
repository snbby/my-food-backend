import React, { useEffect, useState } from 'react';

interface Product {
  id: number;
  product_name: string;
  brands: string;
  countries: string;
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
            <th>Countries</th>
          </tr>
        </thead>
        <tbody>
          {products.map((p) => (
            <tr key={p.id}>
              <td>{p.product_name}</td>
              <td>{p.brands}</td>
              <td>{p.countries}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;
