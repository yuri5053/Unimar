<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

/**
 * @OA\Schema(
 *     schema="Emprestimo",
 *     type="object",
 *     title="Emprestimo",
 *     required={"user_id", "livro_id", "data_emprestimo"},
 *     @OA\Property(
 *         property="id",
 *         type="integer",
 *         format="int64",
 *         description="ID do empréstimo"
 *     ),
 *     @OA\Property(
 *         property="user_id",
 *         type="integer",
 *         description="ID do usuário que pegou o livro"
 *     ),
 *     @OA\Property(
 *         property="livro_id",
 *         type="integer",
 *         description="ID do livro emprestado"
 *     ),
 *     @OA\Property(
 *         property="data_emprestimo",
 *         type="string",
 *         format="date",
 *         description="Data em que o empréstimo foi feito"
 *     ),
 *     @OA\Property(
 *         property="data_devolucao",
 *         type="string",
 *         format="date",
 *         description="Data em que o livro foi devolvido"
 *     )
 * )
 */
class Emprestimo extends Model
{
    use HasFactory;

    protected $fillable = ['user_id', 'livro_id', 'data_emprestimo', 'data_devolucao'];

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function livro()
    {
        return $this->belongsTo(Livro::class);
    }
}
