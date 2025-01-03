import React from 'react';
import { MultiSelect } from '@procore/core-react';

function Example({ ingredientes }) {
    const options = ingredientes.map(ingrediente => ({
        key: ingrediente.codigo,
        name: ingrediente.ingrediente
    }));

    return (
        <MultiSelect
            getId={(item) => item.key}
            getLabel={(item) => item.name}
            options={options}
            value={(item) => item.key}
        />
    );
}

export default Example;