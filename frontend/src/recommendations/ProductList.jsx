import React from 'react';

export default function ProductList({ recommendations }) {
    return (
        <div className="product-list">
            <h3>Рекомендуемые продукты</h3>
            <div className="products-grid">
                {recommendations?.map((product, index) => (
                    <ProductCard key={index} product={product} rank={index + 1} />
                ))}
            </div>
        </div>
    );
}