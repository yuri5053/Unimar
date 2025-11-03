<?php

namespace App\DataAccess;

use App\Models\Livro;

class LivroDataAccess
{
    protected $model;

    public function __construct(Livro $model)
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
        $livro = $this->find($id);
        if ($livro) {
            $livro->update($data);
            return $livro;
        }
        return null;
    }

    public function delete($id)
    {
        $livro = $this->find($id);
        if ($livro) {
            return $livro->delete();
        }
        return false;
    }
}
