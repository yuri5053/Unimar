<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

/**
 * @OA\Schema(
 *     schema="Categoria",
 *     type="object",
 *     title="Categoria",
 *     required={"nome"},
 *     @OA\Property(
 *         property="id",
 *         type="integer",
 *         format="int64",
 *         description="ID da categoria"
 *     ),
 *     @OA\Property(
 *         property="nome",
 *         type="string",
 *         description="Nome da categoria"
 *     )
 * )
 */
class Categoria extends Model
{
    use HasFactory;

    protected $fillable = ['nome'];

    public function livros()
    {
        return $this->hasMany(Livro::class);
    }
}
