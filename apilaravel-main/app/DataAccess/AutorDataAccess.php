<?php

namespace App\DataAccess;

use App\Models\Autor;

class AutorDataAccess
{
    protected $model;

    public function __construct(Autor $model)
    {
        $this->model = $model;
    }

    public function getAll()
    {
        return $this->model->all();
    }

    public function find($id)
    {
        return $this->model->find($id);
    }

    public function create(array $data)
    {
        return $this->model->create($data);
    }

    public function update($id, array $data)
    {
        $autor = $this->find($id);
        if ($autor) {
            $autor->update($data);
            return $autor;
        }
        return null;
    }

    public function delete($id)
    {
        $autor = $this->find($id);
        if ($autor) {
            return $autor->delete();
        }
        return false;
    }
}
