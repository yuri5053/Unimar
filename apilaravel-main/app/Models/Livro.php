<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

/**
 * @OA\Schema(
 *     schema="Livro",
 *     type="object",
 *     title="Livro",
 *     required={"titulo", "autor_id", "categoria_id"},
 *     @OA\Property(
 *         property="id",
 *         type="integer",
 *         format="int64",
 *         description="ID do livro"
 *     ),
 *     @OA\Property(
 *         property="titulo",
 *         type="string",
 *         description="Título do livro"
 *     ),
 *     @OA\Property(
 *         property="autor_id",
 *         type="integer",
 *         description="ID do autor do livro"
 *     ),
 *     @OA\Property(
 *         property="categoria_id",
 *         type="integer",
 *         description="ID da categoria do livro"
 *     )
 * )
 */
class Livro extends Model
{
    use HasFactory;

    protected $fillable = ['titulo', 'autor_id', 'categoria_id'];

    public function autor()
    {
        return $this->belongsTo(Autor::class);
    }

    public function categoria()
    {
        return $this->belongsTo(Categoria::class);
    }

    public function emprestimos()
    {
        return $this->hasMany(Emprestimo::class);
    }
}
