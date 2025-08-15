import React, { useEffect, useState } from 'react';
import './table.css';

interface Product {
  id: number;
  product_name: string;
  brands: string;
  countries: string;
  carbohydrates_100g: number;
  proteins_100g: number;
  fat_100g: number;
}

const LIMIT = 30;

const App: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isLastPage, setIsLastPage] = useState(false);

  const fetchPage = async (off: number) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/foodproducts/search/?limit=${LIMIT}&offset=${off}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data: Product[] = await res.json();

      // If server returns fewer than limit, we’re at the end.
      setIsLastPage(data.length < LIMIT);

      // If next page was requested and came back empty, step back and lock as last.
      if (off > 0 && data.length === 0) {
        setIsLastPage(true);
        setOffset(off - LIMIT);
        // Keep current list; don’t blow away the previous page
        return;
      }

      setProducts(data);
    } catch (e: any) {
      setError(e.message ?? 'Failed to load');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPage(offset);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [offset]);

  const prev = () => setOffset((o) => Math.max(0, o - LIMIT));
  const next = () => {
    if (!isLastPage) setOffset((o) => o + LIMIT);
  };

  return (
    <div>
      <h1>My-food</h1>

      <div className="pager">
        <button onClick={prev} disabled={offset === 0 || loading}>← Prev</button>
        <span className="page-meta">
          Page {Math.floor(offset / LIMIT) + 1}
          {isLastPage ? ' (last)' : ''}
        </span>
        <button onClick={next} disabled={isLastPage || loading}>Next →</button>
      </div>

      {error && <p className="error">Error: {error}</p>}
      {loading && <p>Loading…</p>}

      {!loading && !error && (
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
      )}
    </div>
  );
};

export default App;
