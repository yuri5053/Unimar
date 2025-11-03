<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

/**
 * @OA\Schema(
 *     schema="Autor",
 *     type="object",
 *     title="Autor",
 *     required={"nome"},
 *     @OA\Property(
 *         property="id",
 *         type="integer",
 *         format="int64",
 *         description="ID do autor"
 *     ),
 *     @OA\Property(
 *         property="nome",
 *         type="string",
 *         description="Nome do autor"
 *     )
 * )
 */
class Autor extends Model
{
    use HasFactory;

    protected $fillable = ['nome'];

    public function livros()
    {
        return $this->hasMany(Livro::class);
    }
}
