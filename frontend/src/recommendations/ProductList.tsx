import {FC} from "react";

interface ProductListProps {
    recommendations: string[];
}

function ProductCard(props: { product: string, rank: number, key?: number }) {
    return null;
}

export const ProductList = ({ recommendations }: ProductListProps) => {
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